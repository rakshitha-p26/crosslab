import { MigrationInterface, QueryRunner, TableColumn } from "typeorm";

export class PeerconnectionRefactoringSTATUS implements MigrationInterface {
    async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.addColumn("Peerconnection", new TableColumn({
            name: "status",
            type: "text",
            enum: ['waiting-for-devices', 'connected', 'failed', 'closed']
        }))
    }

    async down(queryRunner: QueryRunner): Promise<any> {
        await queryRunner.dropColumn("Peerconnection", "status")
    }
}