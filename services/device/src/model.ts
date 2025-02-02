import {
    Column,
    Entity,
    PrimaryGeneratedColumn,
    DeleteDateColumn,
    OneToMany,
    TableInheritance,
    ChildEntity,
    ManyToOne,
    OneToOne,
    JoinColumn,
    AfterLoad,
} from 'typeorm'

export function isConcreteDeviceModel(
    device: DeviceOverviewModel
): device is ConcreteDeviceModel {
    return device.type === 'device'
}

export function isDeviceGroupModel(
    device: DeviceOverviewModel
): device is DeviceGroupModel {
    return device.type === 'group'
}

export function isInstantiableCloudDeviceModel(
    device: DeviceOverviewModel
): device is InstantiableCloudDeviceModel {
    return device.type === 'cloud instantiable'
}

export function isInstantiableBrowserDeviceModel(
    device: DeviceOverviewModel
): device is InstantiableBrowserDeviceModel {
    return device.type === 'edge instantiable'
}

export function isInstantiableDeviceModel(
    device: DeviceOverviewModel
): device is InstantiableBrowserDeviceModel | InstantiableCloudDeviceModel {
    return (
        isInstantiableBrowserDeviceModel(device) || isInstantiableCloudDeviceModel(device)
    )
}

@Entity({ name: 'Device' })
@TableInheritance({
    column: {
        type: 'varchar',
        name: 'type',
        enum: ['device', 'group', 'cloud instantiable', 'edge instantiable'],
    },
})
export abstract class DeviceOverviewModel {
    @PrimaryGeneratedColumn('uuid')
    uuid!: string
    @Column()
    name?: string
    @Column({nullable: true})
    description?: string
    @Column()
    type?: 'device' | 'group' | 'cloud instantiable' | 'edge instantiable'
    @Column()
    owner?: string
    @DeleteDateColumn()
    deletedAt?: Date
}

@ChildEntity()
export abstract class InstantiableDeviceOverviewModel extends DeviceOverviewModel {
    @OneToMany(() => ConcreteDeviceModel, (concreteDevice) => concreteDevice.instanceOf, {
        onDelete: 'CASCADE',
        cascade: true,
    })
    instances?: ConcreteDeviceModel[]
}

@ChildEntity('device')
export class ConcreteDeviceModel extends DeviceOverviewModel {
    @Column()
    type?: 'device'
    @Column()
    connected?: boolean
    @OneToMany(() => TimeSlotModel, (timeslot) => timeslot.device, {
        onDelete: 'CASCADE',
        cascade: true,
    })
    announcedAvailability?: TimeSlotModel[]
    @OneToMany(() => AvailabilityRuleModel, (timeslot) => timeslot.device, {
        onDelete: 'CASCADE',
        cascade: true,
    })
    availabilityRules?: AvailabilityRuleModel[]
    @Column()
    experiment?: string
    @Column()
    token?: string
    @OneToMany(() => ServiceModel, (serviceDescription) => serviceDescription.device, {
        onDelete: 'CASCADE',
        cascade: true,
    })
    services?: ServiceModel[]
    @ManyToOne(
        () => InstantiableDeviceOverviewModel,
        (instantiableDevice) => instantiableDevice.instances
    )
    instanceOf?: InstantiableDeviceOverviewModel
}

@ChildEntity('group')
export class DeviceGroupModel extends DeviceOverviewModel {
    @Column()
    type?: 'group'
    @OneToMany(() => DeviceReferenceModel, (deviceReference) => deviceReference.group, {
        onDelete: 'CASCADE',
        cascade: true,
    })
    devices?: DeviceReferenceModel[]
}

@ChildEntity('cloud instantiable')
export class InstantiableCloudDeviceModel extends InstantiableDeviceOverviewModel {
    @Column()
    type?: 'cloud instantiable'
    @Column()
    instantiateUrl?: string
}

@ChildEntity('edge instantiable')
export class InstantiableBrowserDeviceModel extends InstantiableDeviceOverviewModel {
    @Column()
    type?: 'edge instantiable'
    @Column()
    codeUrl?: string
}

@Entity({ name: 'DeviceReference' })
export class DeviceReferenceModel {
    @PrimaryGeneratedColumn()
    id!: number
    @Column()
    url!: string
    @OneToMany(() => ServiceConfigModel, (serviceConfig) => serviceConfig.device, {
        onDelete: 'CASCADE',
        cascade: true,
    })
    config?: ServiceConfigModel[]
    @ManyToOne(() => DeviceGroupModel, (deviceGroup) => deviceGroup.devices)
    group?: DeviceGroupModel
    @DeleteDateColumn()
    deletedAt?: Date
}

@Entity({ name: 'AvailabilityRule' })
export class AvailabilityRuleModel {
    @PrimaryGeneratedColumn()
    id!: number
    @Column()
    available?: boolean
    @Column({ nullable: true })
    start?: number
    @Column({ nullable: true })
    end?: number
    @Column({ nullable: true })
    frequency?: 'HOURLY' | 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'YEARLY'
    @Column({ nullable: true })
    until?: number
    @Column({ nullable: true })
    count?: number
    @ManyToOne(() => ConcreteDeviceModel, (device) => device.availabilityRules)
    device?: ConcreteDeviceModel
    @AfterLoad()
    nullToUndefined() {
        if (this.available == null) this.available = undefined
        if (this.start == null) this.start = undefined
        if (this.end == null) this.end = undefined
        if (this.frequency == null) this.frequency = undefined
        if (this.until == null) this.until = undefined
        if (this.count == null) this.count = undefined
    }
    @DeleteDateColumn()
    deletedAt?: Date
}

@Entity({ name: 'TimeSlot' })
export class TimeSlotModel {
    @PrimaryGeneratedColumn()
    id!: number
    @Column()
    start!: number
    @Column()
    end!: number
    @ManyToOne(() => ConcreteDeviceModel, (device) => device.announcedAvailability)
    device?: ConcreteDeviceModel
    @DeleteDateColumn()
    deletedAt?: Date
}

@Entity({ name: 'Peerconnection' })
export abstract class PeerconnectionModel {
    @PrimaryGeneratedColumn('uuid')
    uuid!: string
    @Column()
    status!: 'waiting-for-devices' | 'connected' | 'failed' | 'closed'
    @OneToOne(() => DeviceReferenceModel, { onDelete: 'CASCADE', cascade: true })
    @JoinColumn()
    deviceA!: DeviceReferenceModel
    @OneToOne(() => DeviceReferenceModel, { onDelete: 'CASCADE', cascade: true })
    @JoinColumn()
    deviceB!: DeviceReferenceModel
    @DeleteDateColumn()
    deletedAt?: Date
}

@Entity({ name: 'ServiceConfig' })
export class ServiceConfigModel {
    @PrimaryGeneratedColumn()
    id!: number
    @Column()
    serviceType?: string
    @Column()
    serviceId?: string
    @Column()
    remoteServiceId?: string
    @Column()
    config?: string
    @ManyToOne(() => DeviceReferenceModel, (deviceReference) => deviceReference.config)
    device?: DeviceReferenceModel
    @DeleteDateColumn()
    deletedAt?: Date
}

@Entity({ name: 'ServiceDescription' })
export class ServiceModel {
    @PrimaryGeneratedColumn()
    id!: number
    @Column()
    description!: string
    @ManyToOne(() => ConcreteDeviceModel, (concreteDevice) => concreteDevice.services)
    device?: ConcreteDeviceModel
}
